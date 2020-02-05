const fs = require('fs')
const path = require('path')

const directory = path.join('.', 'carwow-videos')
const files = fs.readdirSync(directory)

const list = []
const set = new Set()


files.forEach(file => {
    const fullName = path.join(directory, file)
    const content = JSON.parse(fs.readFileSync(fullName).toString())
    const items = content.items
    items.forEach(item => {
        if (item.snippet.channelTitle !== 'carwow') {
            throw new Error(`Video from unexpected channel - ${item.snippet.channelTitle}`)
        }
        const videoId = item.id.videoId
        if (!set.has(videoId)) {
            set.add(videoId)
            list.push({
                id: videoId,
                title: item.snippet.title,
                car: "",
                date: item.snippet.publishedAt
            })
        }
    })
})

console.log(`Number of videos: ${list.length}`)
fs.writeFileSync(path.join(directory, 'all-videos.json'), JSON.stringify(list, null, 2))
