import {Component, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {CalendarOptions, DateSelectArg, EventApi, EventClickArg, FullCalendarComponent} from '@fullcalendar/angular';
import {WebSocketService} from '../../core/services/web-socket/web-socket.service';
import {JobService} from '../job/service/job.service';
import {EventDropArg, EventResizeDoneArg} from '@fullcalendar/interaction';
import {formatDate} from '@angular/common';

@Component({
  selector: 'app-calendar',
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.scss']
})
export class CalendarComponent implements OnInit, OnDestroy {

  varsSub;
  vars;
  currentEventsSub;
  currentEvents: [] = [];

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
    eventDrop: this.handleEventDrop.bind(this),
    eventResize: this.handleEventResize.bind(this),
    datesSet: this.handleEvents.bind(this),
    events: this.currentEvents,
    height: 'parent'
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
      type: 'calendar_select',
      name: this.jobService.jobRoute,
      vars: this.vars,
      start: selectInfo.startStr,
      end: selectInfo.endStr,
      allDay: selectInfo.allDay
    });
  }

  handleEventDrop(dropInfo: EventDropArg) {
    this.webSocketService.sendMessage({
      type: 'calendar_move',
      id: dropInfo.event.id,
      start: dropInfo.event.startStr,
      end: dropInfo.event.endStr,
      allDay: dropInfo.event.allDay
    });
  }

  handleEventResize(resizeInfo: EventResizeDoneArg) {
    this.webSocketService.sendMessage({
      type: 'calendar_move',
      id: resizeInfo.event.id,
      start: resizeInfo.event.startStr,
      end: resizeInfo.event.endStr,
      allDay: resizeInfo.event.allDay
    });
  }

  handleEventClick(clickInfo: EventClickArg) {
    if (confirm(`Are you sure you want to delete the event '${clickInfo.event.title}'`)) {
      // clickInfo.event.remove();
      this.webSocketService.sendMessage({
        type: 'calendar_delete',
        id: clickInfo.event.id
      });
    }
  }

  handleEvents(events: EventApi[]) {
    if (this.currentEventsSub) {
      this.currentEventsSub.unsubscribe();
    }

    this.currentEventsSub = this.webSocketService.getObservable({
      type: 'get_calendar',
      date: formatDate(this.calendarComponent.getApi().getDate(), 'yyyy-MM-ddThh:mm:ssZZZZZ', 'en')
    }).subscribe(m => {this.calendarOptions.events = m.events; });
  }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
    this.currentEventsSub.unsubscribe();
  }


}
