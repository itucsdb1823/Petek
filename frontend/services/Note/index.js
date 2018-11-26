import Api from '../Api'

export default {
  create(data) {
    return Api().post('notes/store', data)
  },
  getNotes(){
    return Api().get('notes')
  },
  getNote(note_id){
    return Api().get('notes/' + note_id)
  }
}
