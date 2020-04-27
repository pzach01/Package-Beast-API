from rest_framework import serializers
from arrangements.models import Arrangement, ContainerLayout, ItemList
from django.utils.timezone import now
from arrangements.Box_Stuff_Python3_Only import box_stuff2 as optimize

from users.models import User
from users.serializers import UserSerializer

class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemList
        fields = ['height', 'width', 'length', 'volume', 'xCenter', 'yCenter', 'zCenter']

class ContainerLayoutSerializer(serializers.ModelSerializer):
    itemList = ItemListSerializer(many=True, read_only=True)

    class Meta:
        model = ContainerLayout
        fields = ['height', 'width', 'length', 'volume', 'cost', 'itemList']
        
class ArrangementSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    
    containerLayout = ContainerLayoutSerializer(many=True, read_only=True)
    class Meta:
        model = Arrangement
        fields = ['id', 'owner', 'created', 'containers', 'items', 'containerLayout']

    def create(self, validated_data):

        arrangement = Arrangement.objects.create(**validated_data)

        containers = validated_data.get('containers')
        items = validated_data.get('items')
        containers = containers.split(',')
        items = items.split(',')
        calculated_containers=optimize.master_calculate_optimal_solution(containers,items)
        print("ccc", calculated_containers)

        containerDictionarys=[]
        print("eee")
        for calculated_container in calculated_containers:
            print("aaa")
            containerDictionarys.append(calculated_container.to_dictionary())

        print("ddd")
        for containerDictionary in containerDictionarys:
            print("yyy")
            containerDictionary.pop('id', None)
            itemLists = containerDictionary.pop('itemList', None)
            containerDictionary.pop('weightCapacity', None)
            print("zzz", containerDictionary)
            print("arrangement", arrangement.containers)
            print("cd", containerDictionary)
            containerLayout = ContainerLayout.objects.create(arrangement=arrangement, **containerDictionary)
            print("qqq")
            for itemList in itemLists:
                print("sup")
                itemList.pop('weight', None)
                ItemList.objects.create(containerLayout=containerLayout, **itemList)
        print("fff", arrangement)
        return arrangement

    def update(self, instance, validated_data):
        instance.containers = validated_data.get('containers', instance.containers)
        instance.items = validated_data.get('items', instance.items)
        ContainerLayout.objects.filter(arrangement=instance).delete()
        containers = instance.containers.split(',')
        items = instance.items.split(',')

        calculated_containers=optimize.master_calculate_optimal_solution(containers,items)

        containerDictionarys=[]
        for calculated_containers in calculated_containers:
            containerDictionarys.append(calculated_containers.to_dictionary())

        for containerDictionary in containerDictionarys:
            containerDictionary.pop('id', None)
            itemLists = containerDictionary.pop('itemList', None)
            containerDictionary.pop('weightCapacity', None)
            containerLayout = ContainerLayout.objects.create(arrangement=instance, **containerDictionary)

            for itemList in itemLists:
                itemList.pop('weight', None)
                ItemList.objects.create(containerLayout=containerLayout, **itemList)

        instance.save()
        return instance