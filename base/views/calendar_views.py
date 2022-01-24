# from django.shortcuts import render
# from django.views.generic import ListView, DetailView
# # from django.views.generic import ListView, DetailView
# from base.models import MenuItem, MenuCategory, MenuTag
# # from base.models import MenuItem, MenuCategory, MenuTag # 今回 追加

import datetime
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import generic
# from base.models import Store, Staff, Schedule

# 他のビュー略


class Calendar(generic.TemplateView):
    template_name = 'pages/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        today = datetime.date.today()

        # どの日を基準にカレンダーを表示するかの処理。
        # 年月日の指定があればそれを、なければ今日からの表示。
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date = today

        # カレンダーは1週間分表示するので、基準日から1週間の日付を作成しておく
        days = [base_date + datetime.timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        # 9時から17時まで1時間刻み、1週間分の、値がTrueなカレンダーを作る
        calendar = {}
        for hour in range(9, 18):
            row = {}
            for day in days:
                row[day] = True
            calendar[hour] = row
            '''
            calendar = {}の中身
            {9: {datetime.date(2020, 1, 8): True,
                datetime.date(2020, 1, 9): True,
                datetime.date(2020, 1, 10): True,
                datetime.date(2020, 1, 11): True,
                datetime.date(2020, 1, 12): True,
                datetime.date(2020, 1, 13): True,
                datetime.date(2020, 1, 14): True},
            10: {datetime.date(2020, 1, 8): True,
                datetime.date(2020, 1, 9): True,
                datetime.date(2020, 1, 10): True,
                datetime.date(2020, 1, 11): True,
                datetime.date(2020, 1, 12): True,
                datetime.date(2020, 1, 13): True,
                datetime.date(2020, 1, 14): True}, .....
            '''

        # カレンダー表示する最初と最後の日時の間にある予約を取得する
        start_time = datetime.datetime.combine(start_day, datetime.time(hour=9, minute=0, second=0))
        end_time = datetime.datetime.combine(end_day, datetime.time(hour=17, minute=0, second=0))
        # for schedule in Schedule.objects.filter(staff=staff).exclude(Q(start__gt=end_time) | Q(end__lt=start_time)):
        #     local_dt = timezone.localtime(schedule.start)
        #     booking_date = local_dt.date()
        #     booking_hour = local_dt.hour
        #     if booking_hour in calendar and booking_date in calendar[booking_hour]:
        #         calendar[booking_hour][booking_date] = False

        # context['staff'] = staff
        context['calendar'] = calendar
        context['days'] = days
        context['start_day'] = start_day
        context['end_day'] = end_day
        context['before'] = days[0] - datetime.timedelta(days=7)
        context['next'] = days[-1] + datetime.timedelta(days=1)
        context['today'] = today
        context['public_holidays'] = settings.PUBLIC_HOLIDAYS
        return context


