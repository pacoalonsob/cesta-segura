# -*- coding: utf-8 -*-
"""
Datos de muestra extraídos manualmente el 2026-08-27 de fichas de producto
públicas de carrefour.es (rutas /supermercado/.../R-.../p, permitidas por
su robots.txt) para demostrar el prototipo.

Esto NO es el resultado de un scraper automático corriendo en este entorno
(este sandbox no tiene acceso de red saliente a dominios arbitrarios).
Es una muestra recogida a mano vía fetch individual, pensada para poblar
la base de datos de demo. El scraper de producción (scraper_carrefour.py)
reproduce esta misma extracción de forma automática y debe ejecutarse en
un servidor/función con salida a internet real.
"""

PRODUCTS = [
    {
        "supermercado": "Carrefour",
        "nombre": "Pechuga de pavo en lonchas Un Momento y Listo Serrano sin gluten sin lactosa 200 g",
        "marca": "Serrano",
        "precio_eur": 3.09,
        "precio_unidad": "15,45 €/kg",
        "formato": "200 g",
        "sin_gluten": True,
        "sin_lactosa": True,
        "alergenos": "Puede contener: Soja",
        "ingredientes": "Pechuga de pavo (60%), agua, almidón, dextrosa, sal, estabilizantes, antioxidantes, aromas y conservadores",
        "url": "https://www.carrefour.es/supermercado/pechuga-de-pavo-en-lonchas-un-momento-y-listo-serrano-sin-gluten-sin-lactosa-200-g/R-530362920/p",
        "notas": None,
    },
    {
        "supermercado": "Carrefour",
        "nombre": "Tomate frito Helios sin gluten pack de 2 tarros de 570 g",
        "marca": "Helios",
        "precio_eur": 3.69,
        "precio_unidad": "3,24 €/kg",
        "formato": "Pack 2x570 g",
        "sin_gluten": True,
        "sin_lactosa": None,  # no declarado explícitamente en la ficha
        "alergenos": "No se detalla información de alérgenos específicos",
        "ingredientes": "Tomate, cebolla, aceite de girasol, azúcar, jarabe de glucosa y fructosa, almidón modificado de maíz, sal, acidulante: ácido cítrico y especias",
        "url": "https://www.carrefour.es/supermercado/tomate-frito-helios-sin-gluten-pack-de-2-tarros-de-570-g/R-prod420473/p",
        "notas": "Sin lactosa no está declarado en la ficha; no asumir sin confirmar.",
    },
    {
        "supermercado": "Carrefour",
        "nombre": "Alubias con verduras Classic Carrefour sin gluten 430 g",
        "marca": "Carrefour",
        "precio_eur": 1.21,
        "precio_unidad": "2,81 €/kg",
        "formato": "430 g",
        "sin_gluten": True,
        "sin_lactosa": None,
        "alergenos": "No se menciona declaración específica de alérgenos",
        "ingredientes": "Alubias (40%), agua, hortalizas (16%) (guisantes, pimiento verde, zanahoria y patata), tomate concentrado, sal, vino blanco, aceite de oliva (1%), perejil y laurel",
        "url": "https://www.carrefour.es/supermercado/alubias-con-verduras-classic-carrefour-sin-gluten-430-g/R-VC4AECOMM-128384/p",
        "notas": "Sin lactosa no está declarado en la ficha; no asumir sin confirmar.",
    },
    {
        "supermercado": "Carrefour",
        "nombre": "Galletas María Gullón sin gluten y sin lactosa 380 g",
        "marca": "Gullón",
        "precio_eur": 3.29,
        "precio_unidad": "8,66 €/kg",
        "formato": "380 g",
        "sin_gluten": True,
        "sin_lactosa": True,
        "alergenos": "Contiene: Soja",
        "ingredientes": "Harina de maíz, aceite vegetal de girasol alto oleico (18%), azúcar, almidón de maíz, harina de arroz, harina de soja, oligofructosa y fibra de guisante",
        "url": "https://www.carrefour.es/supermercado/galletas-maria-gullon-sin-gluten-y-sin-lactosa-380-g/R-651303741/p",
        "notas": "Elaborado específicamente para celíacos según la ficha.",
    },
    {
        "supermercado": "Carrefour",
        "nombre": "Batido de vainilla Carrefour Clasicc sin gluten 1 l",
        "marca": "Carrefour",
        "precio_eur": 1.30,
        "precio_unidad": "1,30 €/l",
        "formato": "1 l",
        "sin_gluten": True,
        "sin_lactosa": False,
        "alergenos": "Leche",
        "ingredientes": "Leche parcialmente desnatada (1,2% MG), permeado lácteo reconstituido (contiene leche), azúcar, aromas, estabilizantes, extracto de vainilla, colorante, vitamina D",
        "url": "https://www.carrefour.es/supermercado/batido-de-vainilla-carrefour-clasicc-sin-gluten-1-l/R-VC4AECOMM-653693/p",
        "notas": "Ejemplo de falso amigo: el nombre/slug solo menciona 'sin gluten', SÍ contiene lactosa (lleva leche). Importante para el filtro.",
    },
    {
        "supermercado": "Carrefour",
        "nombre": "Pan de hogaza Carrefour Extra No Gluten! sin lactosa 300 g",
        "marca": "Carrefour",
        "precio_eur": 2.95,
        "precio_unidad": "9,83 €/kg",
        "formato": "300 g",
        "sin_gluten": True,
        "sin_lactosa": True,
        "alergenos": "Puede contener semillas de sésamo y mostaza",
        "ingredientes": "Agua, almidón de maíz, aceite de girasol alto oleico, harina de arroz, fibras vegetales (psyllium y bambú), azúcar, almidón de tapioca, levadura, almidón de arroz, estabilizantes, proteína de guisante, masa madre inactiva, harinas de trigo sarraceno, mijo y quinoa, sal, conservadores y aromas",
        "url": "https://www.carrefour.es/supermercado/pan-de-hogaza-carrefour-extra-no-gluten-sin-lactosa-300-g/R-VC4AECOMM-681868/p",
        "notas": "Apto para celíacos según ficha.",
    },
    {
        "supermercado": "Carrefour",
        "nombre": "Bebida de avena ecológica EcoCesta sin gluten y sin azúcar añadido brik 1 l",
        "marca": "EcoCesta",
        "precio_eur": 2.69,
        "precio_unidad": "2,69 €/l",
        "formato": "1 l",
        "sin_gluten": True,
        "sin_lactosa": True,
        "alergenos": "Contiene: Cereales que contienen gluten",
        "ingredientes": "Agua, avena* sin gluten 16%, aceite de girasol* prensado en frío, y sal marina (*de cultivo ecológico)",
        "url": "https://www.carrefour.es/supermercado/bebida-de-avena-ecologica-ecocesta-sin-gluten-y-sin-azucar-anadido-brik-1-l/R-prod750083/p",
        "notas": "CONTRADICCIÓN DETECTADA EN LA PROPIA FICHA: se etiqueta 'sin gluten' pero la declaración de alérgenos dice 'Contiene: Cereales que contienen gluten'. Requiere revisión manual antes de marcarlo como seguro — ejemplo real de por qué no basta con confiar en el texto de la web del súper.",
    },
    {
        "supermercado": "Carrefour",
        "nombre": "Lacón cocido al horno en lonchas Carrefour El Mercado sin gluten y sin lactosa 200 g",
        "marca": "Carrefour El Mercado",
        "precio_eur": 2.25,
        "precio_unidad": "11,25 €/kg",
        "formato": "200 g",
        "sin_gluten": True,
        "sin_lactosa": True,
        "alergenos": "No se especifican alérgenos en la ficha",
        "ingredientes": "Paleta de cerdo 93%, sal, dextrosa, emulgentes, gelificantes y conservantes",
        "url": "https://www.carrefour.es/supermercado/lacon-cocido-al-horno-en-lonchas-carrefour-el-mercado-sin-gluten-y-sin-lactosa-200-g/R-VC4AECOMM-180586/p",
        "notas": None,
    },
]
