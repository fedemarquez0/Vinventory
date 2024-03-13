import requests
import random

# Lista de relacion entre vino y estilo musical
def obtener_estilo_musical(variedad):
    vinos_musica = {
        "Cabernet Sauvignon": "Rock Clásico",
        "Merlot": "Pop",
        "Pinot Noir": "Jazz",
        "Chardonnay": "Música Clásica",
        "Sauvignon Blanc": "Música Folk",
        "Riesling": "Música Experimental",
        "Syrah/Shiraz": "Rock Alternativo",
        "Zinfandel": "Blues",
        "Malbec": "Tango",
        "Tempranillo": "Flamenco",
        "Sangiovese": "Ópera",
        "Grenache/Garnacha": "Reggae"
    }

    # Utilizamos el método get para obtener el estilo musical asociado a la variedad.
    estilo_musical = vinos_musica.get(variedad)
    return f'{estilo_musical}'



# Obtencion de url de playlist de Spotify segun un genero musical.
def obtener_url_de_spotify_por_genero(genero_musical):
    # Define tus credenciales de Spotify
    client_id = '45e7ede9ee40499a9d3156577145aa23'
    client_secret = 'd09d0ed3273f497180ff7f1a7bf344b4'

    # Realiza la autenticación para obtener un token de acceso
    token_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(token_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    auth_data = auth_response.json()
    access_token = auth_data['access_token']

    # Realiza la búsqueda de listas de reproducción
    search_url = f'https://api.spotify.com/v1/search?q={genero_musical}&type=playlist&limit=5'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.get(search_url, headers=headers)
    search_results = response.json()

    # Filtra y obtén el enlace de la lista de reproducción encontrada
    if 'playlists' in search_results and search_results['playlists']['items']:
        playlist = search_results['playlists']['items']
        enlace_playlist = playlist[random.randint(0, len(playlist)-1)]['external_urls']['spotify'] #utiliza un random para traer aleatoriamente una playlist de todas las buscadas
        return enlace_playlist
    else:
        return('https://open.spotify.com/playlist/37i9dQZF1DX2UQ1I1FrJsu') #devuelve una playlist por defecto si no encuentra ninguna


# Falta hacer verificacion para que cuando obterner_estilo_musical(variedad) sea None, devuelva directamente https://open.spotify.com/playlist/37i9dQZF1DX2UQ1I1FrJsu