import axios from 'axios'
import { clientStore } from "../store"

export default () => {
  let user = clientStore.getters.user
  if(user !== undefined && user !== null) user = user.token
  let baseURL;
  if(process.env.BASEURL !== null && process.env.BASEURL !== undefined ){
    baseURL = 'https://dummy-server-08.herokuapp.com/api'
  }else{
    baseURL = 'http://localhost:5000/api'
  }
  return axios.create({
    baseURL: baseURL,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'Bearer ' + user
    },
    transformRequest: [(data) => {
      let str = [];
      for(let p in data)
        if (data.hasOwnProperty(p) && data[p])
          str.push(encodeURIComponent(p) + "=" + encodeURIComponent(data[p]));

      clientStore.commit('setLoading', true)
      clientStore.commit('clearError')

      return str.join("&");
    }],
    transformResponse: [(data, headers) => {
      clientStore.commit('setLoading', false)

      return JSON.parse(data)
    }],
  })
}
