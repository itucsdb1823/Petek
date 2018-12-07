import Api from '../Api'

export default {
  create(data) {
    return Api().post('lecturers/store', data)
  },
  getLecturers(){
    return Api().get('lecturers')
  },
  getLecturer(id){
    return Api().get('lecturers/' + id)
  },
  deleteLecturer(lecturer_id){
    return Api().post('delete-lecturer/')
  },
  editLecturer(lecturer){
    return true;
    // return Api().post('notes/')
  }
}
