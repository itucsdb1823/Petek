import Api from '../Api'

export default {
  getUsers(){
    return Api().get('admin/users')
  },
  getUser(slug){
    return Api().get('users/' + slug)
  },
  deleteUser(user_id){
    return Api().post('admin/users/' + user_id + '/delete')
  },
  editUser(user_id, data){
    return Api().post('users/' + user_id + '/update', data)
  },
}
