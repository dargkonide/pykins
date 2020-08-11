import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { LogsComponent} from './logs/logs.component';
import { MaterialModule} from '../../../../../util/material/material.module';
import { MonacoEditorModule } from 'ngx-monaco-editor';
import { FormsModule } from '@angular/forms';
import {JobsRoutingModule} from './jobs-history-routing.module';



@NgModule({
  declarations: [LogsComponent],
  imports: [
    CommonModule,
    JobsRoutingModule,
    MaterialModule,
    FormsModule,
    MonacoEditorModule
  ]
})
export class JobHistoryModule { }
