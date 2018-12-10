import Api from '../Api'

export default {
  deleteNote(note_id){
    return Api().post('admin/notes/' + note_id + '/delete')
  },
  deleteLecturer(lecturer_id){
    return Api().post('admin/delete-lecturer/')
  },
  deleteComment(note_id, comment_id){
    return Api().post('admin/comments/' + comment_id + '/delete')
  },
  editNote(note){
    return Api().post('admin/notes/' + note.id + '/update', note)
  },
  editLecturer(lecturer){
    return true;
    // return Api().post('notes/')
  },
  editUser(user_id, data){
    return Api().post('admin/users/' + user_id + '/update', data)
  }

}
