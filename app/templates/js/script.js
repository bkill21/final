const clientId = '956fffec97a74222bdd9bf92268a747a'
const clientSecret = 'ef4a661c20094c04b0a3a99488b6794e'

let token
let song


async function getToken(){
    const res = await fetch('https://accounts.spotify.com/api/token',{
        method: 'POST',
        body: 'grant_type=client_credentials',
        headers: {
            Authorization : `Basic ${btoa(clientId+':'+clientSecret)}`,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    if (res.ok){
        const data = await res.json()
        return data.access_token
    }
}

(async ()=>{
    token = await getToken()
})()

async function getSongApiCall(track, artist){
    const res = await fetch(`https://api.spotify.com/v1/search?q=${track},${artist}&type=track,artist`,{
        method: 'GET',
        headers:{
            Authorization: `Bearer ${await getToken()}`,
            'Content-Type': 'application/json'
        }
    })
    if(res.ok){
        const data = await res.json()
        return(data.tracks.items[0].preview_url)
    }
}

const songs = document.getElementsByClassName('play_song')
console.log(songs)
for(const song of songs){
    song.addEventListener('click', async ()=>{
        const [track, artist] = song.innerText.split(' - ')
        if(song){
            stopSong()
        }
        playSong(await getSongApiCall(track, artist))
    })
}


function playSong(url){
    song = new Audio(url)
    song.volume = .1
    song.play()
}

function stopSong() {
    song.pause()
}

