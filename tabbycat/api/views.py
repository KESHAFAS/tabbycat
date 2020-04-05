from django.db.models import Prefetch
from dynamic_preferences.api.serializers import PreferenceSerializer
from dynamic_preferences.api.viewsets import PerInstancePreferenceViewSet
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet

from options.models import TournamentPreferenceModel
from participants.models import Institution
from tournaments.mixins import TournamentFromUrlMixin
from tournaments.models import Tournament

from . import serializers
from .mixins import AdministratorAPIMixin, TournamentAPIMixin, TournamentPublicAPIMixin


class APIRootView(AdministratorAPIMixin, GenericAPIView):
    name = "API Root"
    lookup_field = 'slug'
    lookup_url_kwarg = 'tournament_slug'

    def get(self, request, format=None):
        tournaments_create_url = reverse('api-tournament-list', request=request, format=format)
        institution_create_url = reverse('api-global-institution-list', request=request, format=format)
        return Response({
            "_links": {
                "tournaments": tournaments_create_url,
                "institutions": institution_create_url,
            },
        })


class TournamentViewSet(AdministratorAPIMixin, ModelViewSet):
    # Don't use TournamentAPIMixin here, it's not filtering objects by tournament.
    queryset = Tournament.objects.all()
    serializer_class = serializers.TournamentSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'tournament_slug'


class TournamentPreferenceViewSet(TournamentFromUrlMixin, AdministratorAPIMixin, PerInstancePreferenceViewSet):
    queryset = TournamentPreferenceModel.objects.all()
    serializer_class = PreferenceSerializer

    def get_related_instance(self):
        return self.tournament


class BreakCategoryViewSet(TournamentAPIMixin, AdministratorAPIMixin, ModelViewSet):
    serializer_class = serializers.BreakCategorySerializer


class SpeakerCategoryViewSet(TournamentAPIMixin, AdministratorAPIMixin, ModelViewSet):
    serializer_class = serializers.SpeakerCategorySerializer


class BreakEligibilityView(TournamentAPIMixin, AdministratorAPIMixin, RetrieveUpdateAPIView):
    serializer_class = serializers.BreakEligibilitySerializer

    def get_queryset(self):
        return super().get_queryset().prefetch_related('team_set')


class SpeakerEligibilityView(TournamentAPIMixin, AdministratorAPIMixin, RetrieveUpdateAPIView):
    serializer_class = serializers.SpeakerEligibilitySerializer

    def get_queryset(self):
        return super().get_queryset().prefetch_related('speaker_set')


class InstitutionViewSet(TournamentAPIMixin, AdministratorAPIMixin, ModelViewSet):
    serializer_class = serializers.InstitutionSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        return Institution.objects.all().prefetch_related(Prefetch('team_set', queryset=self.tournament.team_set.all()))


class TeamViewSet(TournamentAPIMixin, AdministratorAPIMixin, ModelViewSet):
    serializer_class = serializers.TeamSerializer


class AdjudicatorViewSet(TournamentAPIMixin, AdministratorAPIMixin, ModelViewSet):
    serializer_class = serializers.AdjudicatorSerializer


class GlobalInstitutionViewSet(AdministratorAPIMixin, ModelViewSet):
    serializer_class = serializers.InstitutionSerializer

    def get_queryset(self):
        return Institution.objects.all()


class SpeakerViewSet(TournamentAPIMixin, AdministratorAPIMixin, ModelViewSet):
    serializer_class = serializers.SpeakerSerializer
    tournament_field = "team__tournament"

    def perform_create(self, serializer):
        serializer.save()
