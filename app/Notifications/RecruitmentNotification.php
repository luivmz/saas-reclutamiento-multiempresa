<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Messages\MailMessage;
use Illuminate\Notifications\Notification;

/**
 * Base for process notifications: stored in the database channel and mirrored by mail (log driver in development).
 */
abstract class RecruitmentNotification extends Notification implements ShouldQueue
{
    use Queueable;

    public function __construct()
    {
        $this->afterCommit();
    }

    abstract public function kind(): string;

    abstract public function title(): string;

    abstract public function message(): string;

    abstract public function url(): ?string;

    /**
     * @return list<string>
     */
    public function via(object $notifiable): array
    {
        return ['database', 'mail'];
    }

    public function toMail(object $notifiable): MailMessage
    {
        $mail = (new MailMessage)
            ->subject($this->title())
            ->greeting('Hola')
            ->line($this->message());

        if ($this->url() !== null) {
            $mail->action('Ver detalle', url($this->url()));
        }

        return $mail;
    }

    /**
     * @return array{kind: string, title: string, message: string, url: string|null}
     */
    public function toArray(object $notifiable): array
    {
        return [
            'kind' => $this->kind(),
            'title' => $this->title(),
            'message' => $this->message(),
            'url' => $this->url(),
        ];
    }
}
