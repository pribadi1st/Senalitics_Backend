const express = require('express')
const cors = require('cors')
const { PythonShell } = require('python-shell');
const fs = require('file-system')
const app = express()

const T = require('./twit/index.js')
//cors
app.use(cors())

//extended json
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
//

app.options('*', cors());

//Access python data

async function accessPythonScript(res){
    
    var myPythonScriptPath = './src/python/exec.py';
    var pyshell = new PythonShell(myPythonScriptPath);
    var result = ''
    await pyshell.on('message', function (message) {
        // received a message sent from the Python script (a simple "print" statement)
        result = message.split(' ')
        console.log('result pertama: ',result)
        // var result_1 = parseInt(result[0])
        // var result_2= parseInt(result[1])
        // var total_result = result_1 + result_2
        // var percentage = result_1 > result_2 ? Math.round(result_1/total_result * 100 ) : Math.round(result_2/total_result * 100 )
        // str_result = result_1 > result_2 ? percentage+'% is negative' : percentage+'% is positive'

        let result_data = JSON.parse(fs.readFileSync('result_data.json'))
        let response = {
            result_data
        }
        return res.send(response)
    });
    pyshell.end(function (err) {
        if (err){
            throw err;
        };
    
        console.log('finished');
    }); 
}

app.get('/', async (req, res) => {
    result = await accessPythonScript(res)
})

// trends/place.json?id=1
app.get('/trends', cors(), async (req, res) => {
    await T.get('trends/place', { id: req.query.id, locale: 'en' }, function(err, data, response) {
        return res.send(data)
    }).then( () => {
    })
})

app.get('/tweets', cors(), async (req, res) => {
    await T.get('search/tweets', { q: req.query.q, count: 100, lang: 'en', tweet_mode: 'extended' }, function(err, data, response) {
        return res.send(data)
    }).then( () => {
        
    })
})

app.post('/generate', (req, res) => {
    const { name } = req.body.param
    T.get('search/tweets', { q: name, count: 100, lang: 'en',tweet_mode: "extended" }, function(err, data, response) {
        var { statuses } = data 
        // filter with spesifik key
        // statuses = statuses.map(({created_at, full_text, user, retweet_count}) => ({created_at, full_text, user, retweet_count}))
        // filter remove duplicated key
        //const ids = statuses.map(o => o.full_text)
        //const filtered = statuses.filter(({full_text}, index) => !ids.includes(full_text, index + 1))
        //done

        fs.writeFile('data_source.json', JSON.stringify(statuses), function (err) {
            result = accessPythonScript(res)
            if (err) return console.log(err);
        });
    })
})

app.get

app.listen(3000)