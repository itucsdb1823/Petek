import Api from '../Api'

export default {
  getCourses(){
    return Api().get('courses')
  },
  addCourse(data){
    return Api().post('/admin/courses/store', data)
  },
  editCourse(id, data){
    return Api().post('/admin/courses')
  }
}
