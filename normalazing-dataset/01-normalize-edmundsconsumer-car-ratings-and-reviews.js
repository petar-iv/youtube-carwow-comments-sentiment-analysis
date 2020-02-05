const path = require('path')
const fs = require('fs')
const lineReader = require('line-reader')


const processFile = (filePath, cb) => {
    let firstLine = true
    let header = null

    const entries = []
    let entry = ''

    lineReader.eachLine(filePath, (line, last) => {
        if (firstLine) {
            header = line.split(',').map(part => {
                const trimmed = part.trim()
                if (trimmed) {
                    return trimmed
                }
                return "Index"
            })
            firstLine = false
            return
        }

        if (/^[0-9]+\s*,\s*on/.test(line)) {
            // this is a new entry
            if (entry.length) {
                entries.push(entry)
            }
            entry = line
        } else {
            // same entry continues on a new line
            entry = entry + ' ' + line
        }

        if (last) {
            if (entry.length) {
              entries.push(entry)
            }
            cb(null, header, entries)
        }
    })
}

let counter = 0
const processFiles = (file, files, cb) => {
    if (!file) {
        return cb()
    }
    console.log(`Processing file #${(++counter)} (${path.basename(file)})`)
    processFile(file, (err, header, entries) => {
        if (err) {
          return cb(err)
        }
        let str = header.join(',')
        str += '\n'
        str += entries.join('\n')
        fs.writeFileSync(file, str)
        processFiles(files.pop(), files, cb)
    })
}

const dir = path.join(__dirname, '..', 'datasets', 'normalized-edmundsconsumer-car-ratings-and-reviews')
let files = fs.readdirSync(dir)
files = files.map(file => path.join(dir, file))
processFiles(files.pop(), files, () => {
    console.log('OK')
})
