#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ Function that retrieves the list of all State """
    all_states = []
    for state in storage.all(State).values():
        all_states.append(state.to_dict())
    return jsonify(all_states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):  # sourcery skip: assign-if-exp, reintroduce-else
    """ Function that retrieves a State """
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ Function that deletes a state """
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """ Function that create a state """
    dico = request.get_json

    if dico is None:
        abort(404, description="Not a JSON")

    if 'name' not in dico:
        abort(404, description="Missing name")

    new_state = State(**dico)

    return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):  # sourcery skip: assign-if-exp, reintroduce-else
    """ Function that update a state """
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)

    dico = request.get_json

    if dico is None:
        abort(404, description="Not a JSON")

    for key, value in dico.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()

    return jsonify(state.to_dict()), 200
