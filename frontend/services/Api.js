import axios from 'axios'
import { clientStore } from "../store"
import { baseURL } from '../config';

export default () => {
  return axios.create({
    baseURL: baseURL,
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
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
