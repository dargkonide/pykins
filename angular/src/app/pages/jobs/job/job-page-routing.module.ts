import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { JobService } from './service/job.service';

import { BuildComponent } from './pages/build/build.component';
import { JobPageComponent } from './job-page.component';
import { AuthGuard } from 'src/app/services/auth/AuthGuard ';

const routes: Routes = [
  {
    path: '',
    canActivate: [AuthGuard],
    component: JobPageComponent,
    children: [
      {
        path: '',
        canActivate: [AuthGuard],
        pathMatch: 'full',
        redirectTo: 'history',
      },

      {
        path: 'job',
        canActivate: [AuthGuard],
        loadChildren: () =>
          import('./pages/job/job.module').then((m) => m.JobModule),
      },
      { path: 'build', canActivate: [AuthGuard], component: BuildComponent },
      {
        path: 'history',
        canActivate: [AuthGuard],
        loadChildren: () =>
          import('./pages/history/history-list/history-list.module').then(
            (m) => m.HistoryListModule
          ),
      },
      {
        path: 'history/:runId',
        canActivate: [AuthGuard],
        loadChildren: () =>
          import('./pages/history/job-history/job-history.module').then(
            (m) => m.JobHistoryModule
          ),
      },

      { path: '**', redirectTo: 'history' },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class JobRoutingModule {}
