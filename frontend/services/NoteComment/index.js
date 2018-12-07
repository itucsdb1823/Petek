import Api from '../Api'

export default {
  create(notes_id, data) {
    return Api().post('notes/' + notes_id + '/store', data )
  },
  delete(note_id, comment_id){
    return Api().post('comments/' + comment_id + '/delete')
  }
}
