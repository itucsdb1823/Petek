import Api from '../Api'

export default {
  deleteNote(note_id){
    return Api().post('admin/notes/' + note_id + '/delete')
  },
  deleteEvent(event_id){
    return Api().post('admin/events/' + event_id + '/delete')
  },
  deleteLecturer(lecturer_id){
    return Api().post('admin/lecturers/'+lecturer_id+'/delete')
  },
  deleteComment(note_id, comment_id){
    return Api().post('admin/comments/' + comment_id + '/delete')
  },
  editNote(note){
    return Api().post('admin/notes/' + note.id + '/update', note)
  },
  editEvent(event){
    return Api().post('admin/events/' + event.id + '/update', event)
  },
  editLecturer(lecturer){
    return Api().post('admin/lecturers/'+lecturer.id + '/update', lecturer)
  },
  editUser(user_id, data){
    return Api().post('admin/users/' + user_id + '/update', data)
  },
  deleteUser(user_id){
    return Api().post('admin/users/'+user_id+'/delete')
  },
}
