from rpclib.application import Application
from rpclib.decorator import srpc
from rpclib.protocol.soap import Soap11
from rpclib.service import ServiceBase
from rpclib.model.complex import Iterable
from rpclib.model.primitive import Integer
from rpclib.model.primitive import String
from rpclib.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from difflib import SequenceMatcher
from heapq import nlargest as _nlargest

import os
import json


cars = []
cars.append({"model": "Tesla model S", "chargingtime": 30*60, "autonomy": 560, "img": 'https://sf1.autoplus.fr/wp-content/uploads/autoplus/2020/10/tesla-model-2020-prix-baisse-passe-sous-les-80-000.jpeg'})
cars.append({"model": "Tesla model 3", "chargingtime": 27*60, "autonomy": 380, "img": 'https://www.automobile-propre.com/wp-content/uploads/2017/07/Model-3-Mountain-Pearl.png'})
cars.append({"model": "Tesla model X", "chargingtime": 30*60, "autonomy": 465, "img": 'https://sf2.auto-moto.com/wp-content/uploads/sites/9/2020/07/tesla_model_x_p90d_13.jpg'})
cars.append({"model": "Tesla model Y", "chargingtime": 30*60, "autonomy": 415, "img": 'https://www.largus.fr/images/images/tesla-model-y-retard-1.jpg'})
cars.append({"model": "Renault ZOE", "chargingtime": 45*60, "autonomy": 390, "img": 'https://sf1.auto-moto.com/wp-content/uploads/sites/9/2022/01/renault-zoe-2022-1-750x410.jpg'})
cars.append({"model": "Porsche Taycan", "chargingtime": 30*60, "autonomy": 407, "img": 'https://images.caradisiac.com/logos-ref/modele/modele--porsche-taycan/S7-modele--porsche-taycan.jpg'})
cars.append({"model": "BMW I3", "chargingtime": 33*60, "autonomy": 325, "img": 'https://www.automobile-propre.com/wp-content/uploads/2020/09/BMW-i3-WindMill-002.jpg'})
cars.append({"model": "Peugeot e-208", "chargingtime": 28*60, "autonomy": 340, "img": 'https://www.turbo.fr/sites/default/files/styles/large/public/2019-09/peugeot-e-208-modele.png?itok=05TTXC_Z'})
cars.append({"model": "Kia e-nitro", "chargingtime": 37*60, "autonomy": 300, "img": 'https://www.kia.com/content/dam/kwcms/kme/global/en/assets/vehicles/e-niro/discover/kia-e-niro-gls-my22-two-lifestyles.jpg'})
cars.append({"model": "Audi e-tron", "chargingtime": 33*60, "autonomy": 400, "img": 'https://images.frandroid.com/wp-content/uploads/2019/11/a1915283_medium-1.jpg'})
cars.append({"model": "Renault Twizy", "chargingtime": 60*60, "autonomy": 90, "img": 'https://cdn.motor1.com/images/mgl/GxO7J/s1/4x3/renault-twizy-by-oakley-design.webp'})
cars.append({"model": "Citroën AMI", "chargingtime": (60+51)*60, "autonomy": 70, "img": 'https://sf1.autoplus.fr/wp-content/uploads/autoplus/2021/10/post-ami-flammes-centre.png'})
cars.append({"model": "Hyundai Kona électrique", "chargingtime": 48*60, "autonomy": 400, "img": 'https://cdn.drivek.it/configurator-imgs/cars/fr/800/HYUNDAI/KONA-ELECTRIC/40180_SUV-5-DOORS/hyundai-kona-electric-2021-front-side-1.jpg'})


def get_close_matches_indexes(word, possibilities, n, cutoff):
    result = []
    s = SequenceMatcher()
    s.set_seq2(word)
    for idx, x in enumerate(possibilities):
        s.set_seq1(x)
        if s.real_quick_ratio() >= cutoff and \
           s.quick_ratio() >= cutoff and \
           s.ratio() >= cutoff:
            result.append((s.ratio(), idx))
    result = _nlargest(n, result)

    return [x for score, x in result]


class CarSoapService(ServiceBase):
    @srpc(String, _returns=String)
    def getCars(str):
        print(str)
        tmpArray = []
        for car in cars:
            tmpArray.append(car["model"].lower())
        
        string = str.lower()
        goodEnough = get_close_matches_indexes(string, tmpArray, 5, 0.4)

        res = [cars[i] for i in goodEnough]

        return json.dumps(res)


if __name__=='__main__':
    application = Application([CarSoapService],'spyne.examples.hello.soap', in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())
    wsgi_application = WsgiApplication(application)

    port = int(os.environ.get('PORT', 8000))

    server = make_server('0.0.0.0', port, wsgi_application)

    print("listening on : " + str(port))

    server.serve_forever()
