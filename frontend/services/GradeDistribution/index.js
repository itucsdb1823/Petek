import Api from '../Api'

export default {
  getGradeDistribution(){
    return Api().get('courses')
  },
  getGradeDistributions(){
    return Api().get('courses')
  },
  createGradeDistribution(data){
    return Api().post('add-grade-distribution', data)
  }
}
