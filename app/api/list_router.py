import app.seedwork.presentation.apiflask as apiflask
import json
from typing import Any, Dict
from flask import redirect, render_template, request, session, url_for
from flask import Response, Request

from app.moduls.lists.aplication.querys.get_states import GetEstate
from app.moduls.lists.aplication.services import ListService
from app.moduls.lists.aplication.mappers import MapeadorEstateDTOJson as MapApp
from app.moduls.lists.aplication.commands.create_estate import CreateEstate
from app.seedwork.domain.exceptions import DomainException

from app.seedwork.aplication.commands import execute_command
from app.seedwork.aplication.queries import execute_query

from app.moduls.locations.aplication.commands.create_location import CreateLocation

bp = apiflask.create_blueprint('list_router', '/list_router')

cons_mimetype = 'application/json'

@bp.route("/list", methods=('GET',))
def get_list():
    map_estates = MapApp()
    sr = ListService()
    return map_estates.dto_to_external(sr.get_all_list())

@bp.route("/listQuery", methods=('GET',))
def get_estate_using_query(id=None):
    query_resultado = execute_query(GetEstate(id))
    map_estates = MapApp()
    
    return map_estates.dto_to_external(query_resultado.resultado)

@bp.route("/estate-command", methods=('POST',))
def async_create_state():
    try:
        estate_dict = request.json

        #print("Request.json: ", estate_dict)
        map_estate = MapApp()
        estate_dto = map_estate.external_to_dto(estate_dict)

        command = CreateEstate(estate_dto)
        
        # TODO Reemplaze es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        execute_command(command)
        
        return Response('{}', status=201, mimetype=cons_mimetype)
    except DomainException as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype=cons_mimetype)


@bp.route("/location-command", methods=('POST',))
def async_create_location():
    try:
        estate_dict = request.json

        #print("Request.json: ", estate_dict)
        map_estate = MapApp()
        estate_dto = map_estate.external_to_dto(estate_dict)

        command = CreateLocation(estate_dto)
        
        # TODO Reemplaze es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        execute_command(command)
        
        return Response('{}', status=201, mimetype=cons_mimetype)
    except DomainException as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype=cons_mimetype)