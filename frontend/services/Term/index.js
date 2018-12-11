import Api from '../Api'

export default {
  getTerms(){
    return Api().get('terms')
  },
  addTerm(data){
    return Api().post('/admin/termn/store', data)
  },
  editTerm(id, data){
    return Api().post('/admin/terms')
  }
}
