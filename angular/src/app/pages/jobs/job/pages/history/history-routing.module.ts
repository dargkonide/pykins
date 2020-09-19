import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { JobsHistoryComponent } from './jobs-history/jobs-history.component';

const routes: Routes = [
  { path: '', component: JobsHistoryComponent },
  {
    path: 'id/:runId',
    loadChildren: () =>
      import('./job-history/job-history.module').then(
        (m) => m.JobHistoryModule
      ),
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class HistoryRoutingModule {}
