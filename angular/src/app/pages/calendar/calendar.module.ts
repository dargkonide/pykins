import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CalendarRoutingModule } from './calendar-routing.module';
import { CalendarComponent } from './calendar.component';
import {MatCardModule} from '@angular/material/card';
import {FullCalendarModule} from '@fullcalendar/angular';


@NgModule({
  declarations: [CalendarComponent],
  imports: [
    CommonModule,
    CalendarRoutingModule,
    MatCardModule,
    FullCalendarModule
  ]
})
export class CalendarModule { }
