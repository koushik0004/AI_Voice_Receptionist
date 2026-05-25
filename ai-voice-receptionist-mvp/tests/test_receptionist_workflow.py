from app.core.bootstrap import build_demo_container
from app.core.models import CallEvent, CallSource


def test_missed_call_recovery_calls_back_and_notifies_owner() -> None:
    container = build_demo_container()
    result = container.workflow.handle_missed_call(
        CallEvent(
            business_id="demo-salon",
            call_id="missed-1",
            caller_number="+919900001111",
            source=CallSource.MISSED_CALLBACK,
        )
    )

    assert result.actions == ["callback_queued", "owner_whatsapp_sent"]
    assert container.whatsapp.messages[-1].template == "missed_call_recovery"


def test_booking_flow_collects_missing_name_then_confirms() -> None:
    container = build_demo_container()
    container.workflow.handle_call_started(
        CallEvent(business_id="demo-salon", call_id="call-1", caller_number="+919900001111")
    )

    first = container.workflow.handle_caller_turn("call-1", "Can I book an appointment tomorrow at 5 pm?")
    assert first.actions == ["booking_name_requested"]

    second = container.workflow.handle_caller_turn("call-1", "My name is Sneha")
    assert "booking_created" in second.actions
    assert "Sneha" in second.say
    assert container.whatsapp.messages[-1].template == "booking_confirmation"


def test_structured_faq_answer_sends_summary() -> None:
    container = build_demo_container()
    container.workflow.handle_call_started(
        CallEvent(business_id="demo-restaurant", call_id="call-2", caller_number="+919900001112")
    )

    result = container.workflow.handle_caller_turn("call-2", "What time do you open?")

    assert result.actions == ["faq_answered", "owner_whatsapp_sent"]
    assert "noon" in result.say


def test_faq_variants_are_answered_from_structured_profile() -> None:
    container = build_demo_container()
    container.workflow.handle_call_started(
        CallEvent(business_id="demo-salon", call_id="call-services", caller_number="+919900001115")
    )

    services = container.workflow.handle_caller_turn("call-services", "What services do you offer?")
    location = container.workflow.handle_caller_turn("call-services", "What is your landmark?")

    assert services.actions == ["faq_answered", "owner_whatsapp_sent"]
    assert "haircuts" in services.say
    assert location.actions == ["faq_answered", "owner_whatsapp_sent"]
    assert "Indiranagar" in location.say


def test_faq_question_after_booking_state_does_not_continue_booking() -> None:
    container = build_demo_container()
    container.workflow.handle_call_started(
        CallEvent(business_id="demo-salon", call_id="call-faq-after-booking", caller_number="+919900001116")
    )
    container.workflow.handle_caller_turn(
        "call-faq-after-booking",
        "Can I book an appointment tomorrow at 5 pm?",
    )

    result = container.workflow.handle_caller_turn("call-faq-after-booking", "What time do you close?")

    assert result.actions == ["faq_answered", "owner_whatsapp_sent"]
    assert "10 AM to 8 PM" in result.say
    assert "May I have your name" not in result.say


def test_restaurant_menu_faq_handles_common_food_question() -> None:
    container = build_demo_container()
    container.workflow.handle_call_started(
        CallEvent(business_id="demo-restaurant", call_id="call-menu", caller_number="+919900001117")
    )

    result = container.workflow.handle_caller_turn("call-menu", "Do you have Jain food?")

    assert result.actions == ["faq_answered", "owner_whatsapp_sent"]
    assert "Jain food" in result.say


def test_human_transfer_sends_summary_before_transfer() -> None:
    container = build_demo_container()
    container.workflow.handle_call_started(
        CallEvent(business_id="demo-salon", call_id="call-3", caller_number="+919900001113")
    )

    result = container.workflow.handle_caller_turn("call-3", "Please connect me to a human")

    assert result.actions[0] == "owner_whatsapp_sent"
    assert result.actions[1].startswith("transfer_started:")
    assert container.whatsapp.messages[-1].template == "transfer_summary"


def test_restaurant_booking_does_not_confuse_party_size_for_time() -> None:
    container = build_demo_container()
    container.workflow.handle_call_started(
        CallEvent(business_id="demo-restaurant", call_id="call-4", caller_number="+919900001114")
    )

    result = container.workflow.handle_caller_turn(
        "call-4",
        "Can I book a table for 4 tomorrow at 8 pm? My name is Rahul.",
    )

    assert "booking_created" in result.actions
    assert "tomorrow at 8 pm" in result.say
    assert "for Rahul" in result.say
    assert " at 4." not in result.say
