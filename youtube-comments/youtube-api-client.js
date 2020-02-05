const fs = require('fs')
const key = require('./key')
const { join } = require('path')
const request = require('request')
const MAX_ALLOWED_ITEMS_PER_PAGE = 50


class Client {

    get(directory, path, baseParams, cb) {
        const list = []
        this._getSinglePage(list, directory, path, baseParams, null, 1, err => {
            if (list.length) {
                fs.writeFileSync(path.join(directory, 'all.json'), JSON.stringify(list, null, 2))
            }
            cb(err)
        })
    }

    _getSinglePage(list, directory, path, baseParams, page, iteration, cb) {
        console.log('Iteration #' + iteration)
        const params = Object.assign({}, baseParams)
        params.key = key
        params.maxResults = MAX_ALLOWED_ITEMS_PER_PAGE

        if (page) {
            params.pageToken = page
        }

        const query = Object.keys(params).map(name => `${name}=${params[name]}`).join('&')

        request({
            method: 'GET',
            uri: `https://www.googleapis.com/youtube/v3${path}?${query}`,
            json: true
        }, (err, resp, body) => {
            if (err) {
                err.iteration = iteration
                return cb(err)
            }
            if (resp.statusCode !== 200) {
                err = new Error(`Unexpected status code: ${resp.statusCode}, body: ${body}`)
                err.iteration = iteration
                return cb(err)
            }
            if (!body.items.length) {
                return cb();
            }
            list.push(body.items)
            fs.writeFileSync(join(directory, `iteration-${iteration}.json`), JSON.stringify(body, null, 2))
            this._getSinglePage(list, directory, path, baseParams, body.nextPageToken, iteration + 1, cb)
        })
    }
}

module.exports = Client
