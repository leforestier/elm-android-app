module Main exposing (..)

import Browser
import Html exposing (Html, button, div, text)
import Html.Events exposing (onClick)
import String


main =
    Browser.document
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }


type alias Model =
    { count : Int }


type Msg
    = Increment
    | Reset


init : () -> ( Model, Cmd Msg )
init _ =
    ( { count = 0 }, Cmd.none )


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Increment ->
            ( { model | count = model.count + 1 }, Cmd.none )

        Reset ->
            ( { model | count = 0 }, Cmd.none )


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none


view : Model -> Browser.Document Msg
view model =
    { title = "My title"
    , body =
        [ div
            []
            [ text <| "Count: " ++ String.fromInt model.count ]
        , div
            []
            [ button
                [ onClick Increment ]
                [ text " + " ]
            ]
        , div
            []
            [ button
                [ onClick Reset ]
                [ text " 0 " ]
            ]
        ]
    }
