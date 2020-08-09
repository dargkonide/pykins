import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { JobRoutingModule } from './job-page-routing.module';
import { JobPageComponent } from './job-page.component';
import { HistoryComponent } from './pages/history/history.component';
import { BuildComponent } from './pages/build/build.component';
import { JobComponent } from './pages/job/job.component';
import { MaterialModule } from 'src/app/util/material/material.module';
import { FormsModule } from '@angular/forms';
import {FullCalendarModule} from '@fullcalendar/angular';
import { DeleteJobDialogComponent } from './pages/delete-job-dialog/delete-job-dialog.component';

@NgModule({
  declarations: [JobPageComponent, JobComponent, HistoryComponent, BuildComponent, DeleteJobDialogComponent],
  imports: [
        CommonModule,
        JobRoutingModule,
        MaterialModule,
        FormsModule,
        FullCalendarModule,
    ],
  schemas: [ CUSTOM_ELEMENTS_SCHEMA ]
})
export class JobModule { }
