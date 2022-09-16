#!/usr/bin/python3
""" Method HTTP for City """
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv

@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_all_place_amenities(place_id):
    """ Function that retrieves the list of all Place amenities """
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)

    all_aminities = []
    for amenity in place.aminities:
        all_aminities.append(amenity.to_dict())
    return jsonify(all_aminities)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(amenity_id, place_id):
    """ Function that deletes a review """
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)

    amenity = storage.get(amenity, amenity_id)
    if amenity is None:
        return abort(404)

    if amenity not in place.amenities:
        return abort(404)

    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def place_aminity(place_id, amenity_id):
    """ Function that create a place amenity"""

    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    if getenv('HBNB_MYSQL_DB') == 'db':
        place.amenities.append(amenity)
    elif getenv('HBNB_MYSQL_DB') == 'fs':
        place.amenity_ids.append(amenity.id)
    place.save()
    return jsonify(amenity.to_dict()), 201
