from django.contrib import admin


from .models import Topics
from .models import CustomerSubscription, CustomerClassification, Customer  # CustomerAchievement,
from .models import Tier1Discipline
from .models import Countries
from .models import Regions


# class CustomerSubscriptionInline(admin.StackedInline):
#     model = Customer.subscriptions.through
#
#
# class CustomerClassificationInline(admin.TabularInline):
#     model = Customer.classifications.through
#
#
# class CustomerAchievementsInline(admin.TabularInline):
#     model = Customer.achievements.through
#
#
class CustomerAdmin(admin.ModelAdmin):
    # inlines = [CustomerSubscriptionInline, CustomerClassificationInline, CustomerAchievementsInline, ]
    filter_horizontal = ('subscriptions', 'classifications', )

admin.site.register(Customer, CustomerAdmin)
# admin.site.register(Customer)
admin.site.register(CustomerSubscription)
admin.site.register(CustomerClassification)
# admin.site.register(CustomerAchievement)
admin.site.register(Tier1Discipline)
admin.site.register(Topics)
admin.site.register(Countries)
admin.site.register(Regions)
