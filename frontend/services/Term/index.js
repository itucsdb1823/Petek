import Api from '../Api'

export default {
  getTerms(){
    return Api().get('terms')
  }
}
