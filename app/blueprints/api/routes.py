from flask import request, jsonify

from . import bp
from app.models import Song, User
from app.blueprints.api.helpers import token_required

# Recieve All Songs created
@bp.get('/add_song')
@token_required
def api_songs(user):
    result = []
    songs = Song.query.all()
    for song in songs:
        result.append({
            'id':song.song_id,
            'name':song.song_name, 
            'artist':song.song_artist, 
            'currator':song.user_id,
            'timestamp':song.creation_date
            })
    return jsonify(result), 200

# Recieve songs created by Single User
@bp.get('/add_song/<username>')
@token_required
def user_songs(user, username):
    user = User.query.filter_by(username=username).first()
    if user:
      return jsonify([{
            'id':song.song_id,
            'name':song.song_name, 
            'artist':song.song_artist, 
            'currator':song.user_id,
            'timestamp':song.creation_date
            } for song in user.songs]), 200
    return jsonify([{'message':'Invalid Username'}]), 404 

#Search single song
@bp.get('/add_song/<song_id>')
@token_required
def get_song(user, song_id):
    try:
      song = Song.query.get(song_id)
      return jsonify([{
            'id':song.song_id,
            'name':song.song_name, 
            'artist':song.song_artist, 
            'currator':song.user_id,
            'timestamp':song.creation_date
            }])
    except: 
      return jsonify([{'message':'Invalid Hero Id'}]), 404
    
#Add song
@bp.post('/add_song')
@token_required
def add_song(user):
    try:
        content = request.json
        song = Song(song_name=content.get('song_name'), song_artist=content.get('song_artist'), user_id=user.user_id)
        song.commit()
        return jsonify([{'message':'Song Currated!','song_name':song.song_name}])
    except:
       jsonify([{'message':'invalid form data'}]), 401