import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { JobRoutingModule } from './job-page-routing.module';
import { ComponentsModule } from 'src/app/components/material.module';
import { FormsModule } from '@angular/forms';
import { FullCalendarModule } from '@fullcalendar/angular';

import { JobPageComponent } from './job-page.component';
import { BuildComponent } from './pages/build/build.component';
import { JobComponent } from './pages/job/job.component';
import { DeleteJobDialogComponent } from './pages/delete-job-dialog/delete-job-dialog.component';

@NgModule({
  declarations: [
    JobPageComponent,
    JobComponent,
    BuildComponent,
    DeleteJobDialogComponent,
  ],
  imports: [
    CommonModule,
    JobRoutingModule,
    ComponentsModule,
    FullCalendarModule,
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class JobModule {}
