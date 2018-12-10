import axios from 'axios'
import { clientStore } from "../store"

export default () => {
  let user = clientStore.getters.user
  if(user !== undefined && user !== null) user = user.token
  else user = '';
  console.log("user")
  console.log(user);
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
      clientStore.commit('postRequest', null)
      clientStore.commit('getRequest', null)

      return str.join("&");
    }],
    transformResponse: [(data, headers) => {
      clientStore.commit('setLoading', false)
      try{
        return JSON.parse(data)
      } catch(e){
        return JSON.parse('{\n' +
          '\t\t\t"errors": [\n' +
          '\t\t\t\t"An error has occurred!"\n' +
          '\t\t\t]\n' +
          '}')
      }
    }],
  })
}
