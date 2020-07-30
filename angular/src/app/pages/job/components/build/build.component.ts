import { formatDate } from '@angular/common';
import { Component, OnInit, ViewChild } from '@angular/core';
import { WebSocketService } from 'src/app/core/services/web-socket/web-socket.service';
import { JobService } from '../../service/job.service';
import { FullCalendarComponent, CalendarOptions, DateSelectArg, EventClickArg, EventApi } from '@fullcalendar/angular';
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
      right: 'timeGridWeek,timeGridDay'
    },
    locale: 'ru',
    selectable: true,
    selectMirror: true,
    dayMaxEvents: true,
    select: this.handleDateSelect.bind(this),
    eventClick: this.handleEventClick.bind(this),
    datesSet: this.handleEvents.bind(this),
    events: this.currentEvents,
  };

  @ViewChild('calendar') calendarComponent: FullCalendarComponent;

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
    // console.log();
  }

  handleEventClick(clickInfo: EventClickArg) {
    if (confirm(`Are you sure you want to delete the event '${clickInfo.event.title}'`)) {
      clickInfo.event.remove();
    }
  }

  handleEvents(events: EventApi[]) {
<<<<<<< HEAD
    this.varsSub = this.webSocketService.getObservable({
=======
    if(this.currentEventsSub){
      this.currentEventsSub.unsubscribe()
    }
    this.currentEventsSub = this.webSocketService.getObservable({
>>>>>>> e3e2894048c4ebd7230ac3c1925e82a172629b08
      type: 'get_schedule',
      name: this.jobService.jobRoute,
      date: formatDate(this.calendarComponent.getApi().getDate(), "yyyy-MM-ddThh:mm:ssZZZZZ", "en")
    }).subscribe(
      m => {
<<<<<<< HEAD
        this.currentEvents = m.events;
        console.log('events_set')
      }
    )

=======
        this.calendarOptions.events = m.events;
        console.log('events_set', this.currentEvents)
        // this.calendarComponent.getApi().refetchEvents()
      }
    )
>>>>>>> e3e2894048c4ebd7230ac3c1925e82a172629b08
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
  
  ngOnDestroy(): void {
    this.varsSub.unsubscribe()
  }

  runJob(){
    this.webSocketService.sendMessage({
      type: 'runJob',
      name: this.jobService.jobRoute,
      vars: this.vars
    })
  }

}
