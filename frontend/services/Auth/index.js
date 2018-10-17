import Api from '../Api'

export default {
  register(data) {
    return Api().post('register', data)
  },
  login(data) {
    return Api().post('login', data)
  }
}
