const fs = require('fs')
const path = require('path')
const Client = require('./youtube-api-client')
const videos = require('./carwow-videos/final-videos.json')

if (process.argv.length !== 3) {
    throw new Error('Missing index of video in array of videos')
}

const video = videos[process.argv[2]]
console.log(video.car)

const directory = path.join(__dirname, 'carwow-comments', video.car)
if (fs.existsSync(directory)) {
    throw new Error('Careful! Directory for this video already exists!')
}
fs.mkdirSync(directory)

let client = new Client()
client.get(directory, '/commentThreads', {
    textFormat: 'plainText',
    part: 'snippet',
    videoId: video.id
}, err => {
    if (err) {
        console.log(err)
    } else {
        console.log('OK')
    }
})
