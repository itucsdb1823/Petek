import Api from '../Api'

export default {
  create(data) {
    return Api().post('events/store', data)
  },
  getEvents(){
    return Api().get('events')
  },
  getEvent(event_id){
    return Api().get('events/' + event_id)
  },
  deleteEvent(event_id){
    return Api().post('events/' + event_id + '/delete')
  },
  editEvent(event){
    return Api().post('events/' + event.id + '/update', event)
  }
}
