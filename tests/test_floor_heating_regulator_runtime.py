import asyncio, base64, json, sys, yaml
from datetime import datetime, timezone, timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.script_variables import ScriptVariables
from homeassistant.helpers import template

class Loader(yaml.SafeLoader):
    pass
Loader.add_constructor('!input', lambda loader,node: {'__input__':loader.construct_scalar(node)})
from pathlib import Path
source=base64.b64decode(sys.argv[1]) if len(sys.argv)>1 else (Path(__file__).resolve().parents[1]/'floor_heating_regulator_automation.yaml').read_bytes()
bp=yaml.load(source, Loader=Loader)
def resolve(x, inputs):
    if isinstance(x,dict):
        if set(x)=={'__input__'}:return inputs[x['__input__']]
        return {k:resolve(v,inputs) for k,v in x.items()}
    if isinstance(x,list):return [resolve(v,inputs) for v in x]
    return x
async def main():
    hass=HomeAssistant('/config/.git/hermes-heat-tests')
    inputs={'max_regulator_value':85,'regulator_set_point':'number.test_regulator','climate_entity':'climate.test_heat','statistics_sensor':'sensor.test_mean','temperature_sensor':'sensor.test_temperature','temperature_last_seen':'sensor.test_last_seen','outdated_threshold_hours':5,'outdated_temperature_actions':[]}
    variables=resolve(bp['actions'][0]['variables'],inputs)
    from homeassistant.helpers import config_validation as cv
    variables=cv.template_complex(variables)
    cases=[
        ('below_target',{},85),
        ('at_target',{'temperature':25,'average':25},15),
        ('stale',{'age':6},0),
        ('missing_last_seen',{'last_seen':'unavailable'},0),
        ('invalid_source',{'source':'unavailable'},0),
        ('invalid_mean',{'average':'unavailable'},0),
        ('invalid_target',{'target':None},0),
        ('invalid_current',{'temperature':None},0),
        ('nonnumeric_source',{'source':'broken'},0),
        ('off',{'mode':'off'},85),
        ('loft_below_target',{'temperature':20.8,'target':21,'average':20.81,'max':50},50),
        ('basement_at_target',{'temperature':24,'target':24,'average':24,'max':60},10),
    ]
    from homeassistant.helpers.script import Script, async_validate_actions_config
    calls=[]
    async def record(call):
        calls.append(call.data)
    hass.services.async_register('number','set_value',record)
    actions=await async_validate_actions_config(hass,cv.SCRIPT_SCHEMA(resolve(bp['actions'],inputs)))
    for name,override,expected in cases:
        d={'temperature':21.3,'target':25,'average':21.3,'age':0,'source':'21.3','mode':'heat','max':85,**override}
        hass.states.async_set('number.test_regulator','34')
        hass.states.async_set('climate.test_heat',d['mode'],{'current_temperature':d['temperature'],'temperature':d['target']})
        hass.states.async_set('sensor.test_temperature',d['source'])
        hass.states.async_set('sensor.test_mean',d['average'])
        stamp=d.get('last_seen',(datetime.now(timezone.utc)-timedelta(hours=d['age'])).isoformat())
        hass.states.async_set('sensor.test_last_seen',stamp)
        v=ScriptVariables(variables).async_render(hass,{'max_regulator_value':d['max']})
        # Blueprint max is an input constant; set the resolved variable per case.
        if d['max']!=85:
            vv=dict(variables);vv['max_regulator_value']=d['max'];v=ScriptVariables(vv).async_render(hass,{})
        assert v['regulator_output_value']==expected,(name,v)
        if name=='off':assert v['heating_disabled'] is True
        if name in ['stale','missing_last_seen','invalid_source','invalid_mean','invalid_target','invalid_current','nonnumeric_source']:assert v['has_error'] is True
        calls.clear()
        case_inputs=dict(inputs,max_regulator_value=d['max'])
        case_actions=await async_validate_actions_config(hass,cv.SCRIPT_SCHEMA(resolve(bp['actions'],case_inputs)))
        await Script(hass,case_actions,'isolated floor heat test','automation').async_run({})
        expected_service=0 if d['mode']=='off' else expected
        assert len(calls)==1 and float(calls[0]['value'])==expected_service,(name,calls)
        print(json.dumps({'test':name,'output':v['regulator_output_value'],'service_value':expected_service,'has_error':v['has_error'],'heating_disabled':v['heating_disabled']}))
    # Off action has precedence over computed demand, and error notifications are nested under safety-off.
    actions=resolve(bp['actions'],inputs)
    assert actions[1]['choose'][0]['sequence'][0]['then'][0]['data']['value']=='0'
    assert actions[1]['choose'][1]['sequence'][1]['then'][1]['default']==[]
    print('PASS: 12 installed-runtime variable cases; off-action and notification structure')
    await hass.async_stop()
asyncio.run(main())
