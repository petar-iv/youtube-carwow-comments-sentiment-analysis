const Client = require('./youtube-api-client')

const CARWOW_CHANNEL_ID = 'UCUhFaUpnq31m6TNX2VKVSVA'

let client = new Client()
client.get("carwow-videos", '/search', {
    channelId: CARWOW_CHANNEL_ID,
    part: 'id,snippet',
    order: 'date',
    type: 'video'
}, err => {
    if (err) {
        console.log(err)
    } else {
        console.log('OK')
    }
})
