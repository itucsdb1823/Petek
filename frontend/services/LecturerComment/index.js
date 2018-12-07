import Api from '../Api'

export default {
  create(lecturer_id, data) {
    return Api().post('lecturers/' + lecturer_id + '/store', data )
  },
  delete(note_id, comment_id){
    return Api().post('comments/' + comment_id + '/delete')
  }
}
