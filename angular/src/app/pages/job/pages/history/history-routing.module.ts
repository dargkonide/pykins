import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { JobHistoryComponent } from './job-history/job-history.component';
import { JobsHistoryComponent } from './jobs-history/jobs-history.component';



const routes: Routes = [
    { path: '', component: JobsHistoryComponent },
    { path: 'id/:runId', component: JobHistoryComponent },
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HistoryRoutingModule { }
