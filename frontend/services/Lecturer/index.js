import Api from '../Api'

export default {
  create(data) {
    return Api().post('add-lecturer', data)
  },
  getLecturers(){
    return Api().get('get-lecturers')
  },
  getLecturer(slug){
    return Api().get('get-lecturer/' + slug)
  },
  deleteLecturer(lecturer_id){
    return Api().post('delete-lecturer/')
  },
  editLecturer(lecturer){
    return true;
    // return Api().post('notes/')
  }
}
