import { Component, OnInit } from '@angular/core';
import { WebSocketService } from 'src/app/core/services/web-socket/web-socket.service';
import { JobService } from '../../service/job.service';
import { CalendarOptions, DateSelectArg, EventClickArg, EventApi } from '@fullcalendar/angular';
@Component({
  selector: 'app-build',
  templateUrl: './build.component.html',
  styleUrls: ['./build.component.scss']
})
export class BuildComponent implements OnInit {

  varsSub
  vars
  calendarOptions: CalendarOptions = {
    initialView: 'timeGridWeek',
    firstDay: 1,
    editable: true,
    navLinks: true,
    droppable: true,
    nowIndicator: true,
    dayHeaders: true,
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
    },
    locale: 'ru',
    selectable: true,
    selectMirror: true,
    dayMaxEvents: true,
    select: this.handleDateSelect.bind(this),
    eventClick: this.handleEventClick.bind(this),
    eventsSet: this.handleEvents.bind(this)
  };

  currentEvents: EventApi[] = [];

  constructor(
    private webSocketService: WebSocketService,
    private jobService: JobService
  ) { }

  handleDateSelect(selectInfo: DateSelectArg) {
    const calendarApi = selectInfo.view.calendar;
    calendarApi.unselect(); // clear date selection
    this.webSocketService.sendMessage({
      type: 'schedule_select',
      name: this.jobService.jobRoute,
      vars: this.vars,
      start: selectInfo.startStr,
      end: selectInfo.endStr,
      allDay: selectInfo.allDay
    })
  }

  handleEventClick(clickInfo: EventClickArg) {
    if (confirm(`Are you sure you want to delete the event '${clickInfo.event.title}'`)) {
      clickInfo.event.remove();
    }
  }

  handleEvents(events: EventApi[]) {
    this.currentEvents = events;
  }



  ngOnInit(): void {
    this.varsSub = this.webSocketService.getObservable({
      type: 'build',
      name: this.jobService.jobRoute
    }).subscribe(
      m => {
        this.vars = m.msg
        console.log(m)
      }
    )
  }

  runJob(){
    this.webSocketService.sendMessage({
      type: 'runJob',
      name: this.jobService.jobRoute,
      vars: this.vars
    })
  }

}
