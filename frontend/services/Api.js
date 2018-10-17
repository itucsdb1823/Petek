import axios from 'axios'

export default () => {
    return axios.create({
        baseURL: 'http://localhost:5000/api',
        transformResponse: data => JSON.parse(data)
    })
}
