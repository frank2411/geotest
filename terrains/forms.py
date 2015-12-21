from django import forms
from terrains.models import TerrainImport, Circonscription


class TerrainImportAdminForm(forms.ModelForm):

    def clean_csvfile(self):
        csvfile = self.cleaned_data.get("csvfile")
        if not csvfile:
            return csvfile

        name, ext = csvfile.name.split(".")
        if ext != "csv":
            raise forms.ValidationError(
                "Unvalid file extension"
            )

        return csvfile

    class Meta:
        model = TerrainImport
        fields = ("csvfile", )


class CirconscriptionSearchForm(forms.Form):
    circonscriptions = forms.ChoiceField(
        label="Circonscriptions",
        choices=[
            (x, y) for x, y in Circonscription.objects.filter(
                provcode="QC").values_list(
                "fednum", "frname").order_by("enname")
        ],
        required=False
    )
