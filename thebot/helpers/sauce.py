import aiohttp

airing_query = '''
    query ($id: Int,$search: String) {
        Media (id: $id, type: ANIME,search: $search) {
            id
            episodes
            title {
                romaji
                english
                native
                }
            nextAiringEpisode {
                airingAt
                timeUntilAiring
                episode
            } 
        }
    }
'''

fav_query = """
query ($id: Int) {
    Media (id: $id, type: ANIME) { 
        id
        title {
            romaji
            english
            native
        }
    }
}
"""

anime_query = '''
query ($id: Int,$search: String) {
    Media (id: $id, type: ANIME,search: $search) {
        id
    title {
        romaji
        english
        native
    }
    description (asHtml: false)
    startDate{
        year
        }
        episodes
        season
        type
        format
        status
        duration
        siteUrl
        studios{
            nodes{
                name
            }
        }
        trailer{
            id
            site
            thumbnail
        }
        averageScore
        genres
        bannerImage
    }
}
'''

character_query = """
    query ($query: String) {
        Character (search: $query) {
            id
            name {
                first
                last
                full
            }
            siteUrl
            image {
                large
            }
            description
        }
    }
"""

manga_query = """
query ($id: Int,$search: String) { 
    Media (id: $id, type: MANGA,search: $search) { 
        id
        title {
            romaji
            english
            native
        }
        description (asHtml: false)
        startDate{
            year
        }
        type
        format
        status
        siteUrl
        averageScore
        genres
        bannerImage
    }
}
"""

url = 'https://graphql.anilist.co'


async def airing(variables):
    async with aiohttp.ClientSession() as ses:
        async with ses.post(
            url, json={'query': airing_query, 'variables': variables}
        ) as resp:
            response = await resp.json()
        return response['data']['Media']


async def anime(variables):
    async with aiohttp.ClientSession() as ses:
        async with ses.post(url, json={'query': anime_query, 'variables': variables}) as resp:
            response = await resp.json()
        return response['data'].get('Media', None)


async def character(variables):
    async with aiohttp.ClientSession() as ses:
        async with ses.post(
            url, json={'query': character_query, 'variables': variables}
        ) as resp:
            response = await resp.json()
        return response['data'].get('Character', None)


async def manga(variables):
    async with aiohttp.ClientSession() as ses:
        async with ses.post(
            url, json={'query': manga_query, 'variables': variables}
        ) as resp:
            response = await resp.json()
        return response['data'].get('Media', None)