import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import {
  CalendarOptions,
  EventApi,
  FullCalendarComponent,
} from '@fullcalendar/angular';
import { AuthSocketService } from 'src/app/services/auth-socket/auth-socket.service';
import { formatDate } from '@angular/common';

@Component({
  selector: 'app-calendar',
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.scss'],
})
export class CalendarComponent implements OnInit, OnDestroy {
  varsSub;
  vars;
  currentEventsSub;
  currentEvents: [] = [];

  calendarOptions: CalendarOptions = {
    initialView: 'timeGridWeek',
    firstDay: 1,
    editable: false,
    navLinks: true,
    droppable: false,
    nowIndicator: true,
    dayHeaders: true,
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'timeGridWeek,timeGridDay',
    },
    locale: 'ru',
    selectable: false,
    selectMirror: true,
    dayMaxEvents: true,
    datesSet: this.handleEvents.bind(this),
    events: this.currentEvents,
    height: 'parent',
  };

  @ViewChild('calendar') calendarComponent: FullCalendarComponent;

  constructor(private authSocketService: AuthSocketService) {
    this.authSocketService.connect();
  }

  handleEvents(events: EventApi[]) {
    if (this.currentEventsSub) {
      this.currentEventsSub.unsubscribe();
    }

    this.currentEventsSub = this.authSocketService
      .getObservable({
        type: 'get_calendar',
        date: formatDate(
          this.calendarComponent.getApi().getDate(),
          'yyyy-MM-ddThh:mm:ssZZZZZ',
          'en'
        ),
      })
      .subscribe((m) => {
        this.calendarOptions.events = m.events;
      });
  }

  ngOnInit(): void {}

  ngOnDestroy(): void {
    this.currentEventsSub.unsubscribe();
  }
}
