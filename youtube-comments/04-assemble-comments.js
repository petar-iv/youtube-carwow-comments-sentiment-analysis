const fs = require('fs')
const path = require('path')

const rootDirectory = path.join('.', 'carwow-comments')
const cars = fs.readdirSync(rootDirectory)

const allComments = {}
for(car of cars) {
    allComments[car] = []
    const carDirectory = path.join(rootDirectory, car)
    const commentsFiles = fs.readdirSync(carDirectory)
    const commentIdSet = new Set()
    const commentTextSet = new Set()
    commentsFiles.forEach(file => {
        const fullFilePath = path.join(carDirectory, file)
        var content = JSON.parse(fs.readFileSync(fullFilePath))
        content.items.forEach(item => {
            const comment = item.snippet.topLevelComment
            const id = comment.id
            const text = comment.snippet.textOriginal
            const author = comment.snippet.authorDisplayName

            if (!text) {
                return
            }

            if (commentIdSet.has(id) && !commentTextSet.has(text)) {
                throw new Error('Inconsistency! We expect that the comment\'s text is unique just like the comment\'s id')
            } else {
                commentIdSet.add(id)
                commentTextSet.add(text)
                allComments[car].push({
                    author,
                    text
                })
            }
        })
    })

    console.log(allComments[car].length + ' comments for car ' + car)
}

fs.writeFileSync(path.join(rootDirectory, 'all-comments.json'), JSON.stringify(allComments, null, 2))
